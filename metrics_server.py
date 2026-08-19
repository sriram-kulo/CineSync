from prometheus_client import start_http_server, Gauge, Counter
import random
import time

# CineSync production metrics
render_queue = Gauge(
    "cinesync_render_queue_depth",
    "Number of scenes waiting for rendering"
)

camera_latency = Gauge(
    "cinesync_camera_latency_seconds",
    "Camera ingest latency in seconds"
)

storage_usage = Gauge(
    "cinesync_storage_usage_ratio",
    "Studio storage utilization ratio"
)

render_failures = Counter(
    "cinesync_render_failures_total",
    "Total number of failed renders"
)

active_scenes = Gauge(
    "cinesync_active_scenes",
    "Number of scenes currently being processed"
)

print("Starting CineSync metrics server on http://localhost:8000/metrics")

start_http_server(8000)

while True:
    # Simulate live production telemetry
    queue = random.randint(5, 100)
    latency = round(random.uniform(0.2, 6.0), 2)
    storage = round(random.uniform(0.55, 0.95), 3)
    scenes = random.randint(1, 20)

    render_queue.set(queue)
    camera_latency.set(latency)
    storage_usage.set(storage)
    active_scenes.set(scenes)

    # Occasionally simulate a render failure
    if random.random() < 0.15:
        render_failures.inc()

    print(
        f"queue={queue} "
        f"latency={latency}s "
        f"storage={storage} "
        f"active_scenes={scenes}"
    )

    time.sleep(10)