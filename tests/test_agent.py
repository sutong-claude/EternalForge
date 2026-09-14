"""Basic tests for the agent skeleton."""

from src.core.agent import Agent


def test_agent_can_plan():
    agent = Agent()
    task = agent.plan()
    assert isinstance(task, str)
    assert len(task) > 0
