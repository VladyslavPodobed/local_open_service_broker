from grafana_foundation_sdk.builders.dashboard import Dashboard, Row
from grafana_foundation_sdk.builders import prometheus, timeseries
from grafana_foundation_sdk.cog.encoder import JSONEncoder
from grafana_foundation_sdk.models.common import TimeZoneBrowser
from grafana_foundation_sdk.models import units


def postgres_dashboard() -> Dashboard:
    builder = (
        Dashboard("Postgres")
        .uid("postgres")
        .tags(["generated", "postgres"])
        .refresh("1m")
        .time("now-30m", "now")
        .timezone(TimeZoneBrowser)
        .with_row(Row("connect_to_postgres"))
        .with_panel(
            timeseries.Panel()
            .title("could connect to postgres")
            .unit(units.BitsPerSecondSI)
            .min(0)
            .with_target(
                prometheus.Dataquery()
                .expr(
                    'pg_up'
                )
                .legend_format("{{ device }}")
            )
        )
    )

    return builder


postgres_dashboard = postgres_dashboard().build()
encoder = JSONEncoder(sort_keys=True, indent=2)

with open('./grafana/provisioning/dashboards/postgres_dashboad.json', 'w') as config_file:
    config_file.write(encoder.encode(postgres_dashboard))
