"""Helpers shared by the browser tests."""
from __future__ import annotations

VIEWER = "/projects/ale/viewer/"
CHROMIUM_ARGS = ["--use-angle=swiftshader", "--enable-unsafe-swiftshader", "--ignore-gpu-blocklist"]


def throttle(page, mbps: float = 20.0, latency_ms: int = 20) -> None:
    """Emulate a connection of the given bandwidth through the DevTools protocol."""
    cdp = page.context.new_cdp_session(page)
    cdp.send("Network.enable")
    cdp.send("Network.emulateNetworkConditions", {
        "offline": False, "latency": latency_ms,
        "downloadThroughput": mbps * 1e6 / 8, "uploadThroughput": mbps * 1e6 / 8,
    })


def wait_ready(page, timeout: int = 20000) -> None:
    page.wait_for_function("window.aleViewer && window.aleViewer.ready === true", timeout=timeout)


def stage_centre(page) -> tuple[float, float]:
    box = page.locator("#stage").bounding_box()
    return box["x"] + box["width"] / 2, box["y"] + box["height"] / 2


def drag(page, dx: float, dy: float, steps: int = 12) -> None:
    cx, cy = stage_centre(page)
    page.mouse.move(cx, cy)
    page.mouse.down()
    page.mouse.move(cx + dx, cy + dy, steps=steps)
    page.mouse.up()


def gpu_name(page) -> str:
    return page.evaluate("""() => {
      const gl = aleViewer.renderer.getContext();
      const ext = gl.getExtension('WEBGL_debug_renderer_info');
      return ext ? gl.getParameter(ext.UNMASKED_RENDERER_WEBGL) : gl.getParameter(gl.RENDERER);
    }""")
