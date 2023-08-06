import threading
from contextlib import contextmanager
from typing import Any, Generator, Tuple

import uvicorn
from prometheus_client.core import REGISTRY, CounterMetricFamily
from prometheus_client.exposition import make_asgi_app

from dmarc_metrics_exporter.dmarc_event import Disposition, Meta
from dmarc_metrics_exporter.dmarc_metrics import DmarcMetricsCollection


class Server:
    def __init__(self, exporter: "PrometheusExporter", listen_addr: str, port: int):
        self.exporter = exporter
        config = uvicorn.Config(make_asgi_app(), host=listen_addr, port=port)
        self.server = uvicorn.Server(config)
        self.host = config.host
        self.port = port
        self._main_loop = None

    async def __aenter__(self):
        REGISTRY.register(self.exporter)
        config = self.server.config
        if not config.loaded:
            config.load()
        self.server.lifespan = config.lifespan_class(config)
        await self.server.startup()
        self._main_loop = self.server.main_loop()
        return self

    async def __aexit__(self, exc_type, exc, traceback):
        self.server.should_exit = True
        await self._main_loop
        self._main_loop = None
        await self.server.shutdown()
        REGISTRY.unregister(self.exporter)


class PrometheusExporter:
    LABELS = ("reporter", "from_domain", "dkim_domain", "spf_domain")

    def __init__(self, metrics: DmarcMetricsCollection):
        self._metrics_lock = threading.Lock()
        self._metrics = metrics

    def start_server(self, listen_addr="127.0.0.1", port=9119) -> Server:
        return Server(self, listen_addr, port)

    @contextmanager
    def get_metrics(self) -> Generator[DmarcMetricsCollection, None, None]:
        with self._metrics_lock:
            yield self._metrics

    def collect(self) -> Tuple[Any, ...]:
        dmarc_total = CounterMetricFamily(
            "dmarc_total", "Total number of reported messages.", labels=self.LABELS
        )
        dmarc_compliant_total = CounterMetricFamily(
            "dmarc_compliant_total",
            "Total number of DMARC compliant messages.",
            labels=self.LABELS,
        )
        dmarc_quarantine_total = CounterMetricFamily(
            "dmarc_quarantine_total",
            "Total number of quarantined messages.",
            labels=self.LABELS,
        )
        dmarc_reject_total = CounterMetricFamily(
            "dmarc_reject_total",
            "Total number of rejected messages.",
            labels=self.LABELS,
        )
        dmarc_spf_aligned_total = CounterMetricFamily(
            "dmarc_spf_aligned_total",
            "Total number of SPF algined messages.",
            labels=self.LABELS,
        )
        dmarc_spf_pass_total = CounterMetricFamily(
            "dmarc_spf_pass_total",
            "Total number of messages with raw SPF pass.",
            labels=self.LABELS,
        )
        dmarc_dkim_aligned_total = CounterMetricFamily(
            "dmarc_dkim_aligned_total",
            "Total number of DKIM algined messages.",
            labels=self.LABELS,
        )
        dmarc_dkim_pass_total = CounterMetricFamily(
            "dmarc_dkim_pass_total",
            "Total number of messages with raw DKIM pass.",
            labels=self.LABELS,
        )
        with self._metrics_lock:
            for meta, metrics in self._metrics.items():
                labels = self._meta2labels(meta)
                dmarc_total.add_metric(labels, metrics.total_count)
                dmarc_compliant_total.add_metric(labels, metrics.dmarc_compliant_count)
                dmarc_quarantine_total.add_metric(
                    labels, metrics.disposition_counts.get(Disposition.QUARANTINE, 0)
                )
                dmarc_reject_total.add_metric(
                    labels, metrics.disposition_counts.get(Disposition.REJECT, 0)
                )
                dmarc_spf_aligned_total.add_metric(labels, metrics.spf_aligned_count)
                dmarc_spf_pass_total.add_metric(labels, metrics.spf_pass_count)
                dmarc_dkim_aligned_total.add_metric(labels, metrics.dkim_aligned_count)
                dmarc_dkim_pass_total.add_metric(labels, metrics.dkim_pass_count)
        return (
            dmarc_total,
            dmarc_compliant_total,
            dmarc_quarantine_total,
            dmarc_reject_total,
            dmarc_spf_aligned_total,
            dmarc_spf_pass_total,
            dmarc_dkim_aligned_total,
            dmarc_dkim_pass_total,
        )

    @classmethod
    def _meta2labels(cls, meta: Meta) -> Tuple[str, ...]:
        return tuple(getattr(meta, label) for label in cls.LABELS)
