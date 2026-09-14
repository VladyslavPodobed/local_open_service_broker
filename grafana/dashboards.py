from os import stat
from grafana_foundation_sdk.builders.dashboard import Dashboard, Row
from grafana_foundation_sdk.builders import prometheus, timeseries, stat, gauge
from grafana_foundation_sdk.cog.encoder import JSONEncoder
from grafana_foundation_sdk.models.common import TimeZoneBrowser
from grafana_foundation_sdk.models import units


def postgres_dashboard() -> Dashboard:
    builder = (
        Dashboard("Postgres")
        .uid("postgres")
        .tags(["postgres", "db"])
        .refresh("1m")
        .time("now-60m", "now")
        .timezone(TimeZoneBrowser)

        .with_row(Row("availability"))
        .with_panel(
            stat.Panel()
            .title("postgres is up/down")
            .unit(units.NoUnit)
            .min(0)
            .with_target(
                prometheus.Dataquery()
                .expr('pg_up')
                .legend_format("{{ device }}")
            )
        )

        .with_row(Row("storage"))
        .with_panel(
            timeseries.Panel()
            .title("size of tables")
            .unit(units.Terabytes)
            .min(0)
            .with_target(
                prometheus.Dataquery()
                .expr('pg_database_size_bytes')
                .legend_format("{{ device }}")
            )
        )
    )
    return builder


def host_machine_dashboard() -> Dashboard:
    builder = (
        Dashboard("Host machine info")
        .uid("host_machine")
        .tags(["host"])
        .refresh("1m")
        .time("now-60m", "now")
        .timezone(TimeZoneBrowser)

        .with_row(Row("host machine"))
        .with_panel(
            gauge.Panel()
            .title("cpu load")
            .unit(units.PercentUnit)
            .min(0)
            .max(100)
            .with_target(
                prometheus.Dataquery()
                .expr('100 - (avg by (instance) (rate(node_cpu_seconds_total{mode="idle"}[5m])) * 100)')
                .legend_format("{{ device }}")
            )
        )
    )
    return builder


postgres_dashboard = postgres_dashboard().build()
host_machine_dashboard = host_machine_dashboard().build()
encoder = JSONEncoder(sort_keys=True, indent=2)

with open('./grafana/provisioning/dashboards/postgres_dashboad.json', 'w') as config_file:
    config_file.write(encoder.encode(postgres_dashboard))

with open('./grafana/provisioning/dashboards/host_machine_dashboad.json', 'w') as config_file:
    config_file.write(encoder.encode(host_machine_dashboard))

