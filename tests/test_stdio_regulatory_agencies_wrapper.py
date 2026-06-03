from __future__ import annotations

from src.mcp_server import stdio_server


def test_stdio_search_regulatory_updates_forwards_agencies(monkeypatch) -> None:
    captured = {}

    def fake_call_tool(tool_name: str, **kwargs):
        captured["tool_name"] = tool_name
        captured["kwargs"] = kwargs
        return {"ok": True}

    monkeypatch.setattr(stdio_server, "_call_tool", fake_call_tool)

    result = stdio_server.search_regulatory_updates(
        agencies=["TFDA"],
        query="藥品 查驗登記",
        date_range="1y",
        limit=5,
    )

    assert result == {"ok": True}
    assert captured["tool_name"] == "search_regulatory_updates"
    assert captured["kwargs"]["agency"] is None
    assert captured["kwargs"]["agencies"] == ["TFDA"]
    assert captured["kwargs"]["query"] == "藥品 查驗登記"
    assert captured["kwargs"]["date_range"] == "1y"
    assert captured["kwargs"]["limit"] == 5
