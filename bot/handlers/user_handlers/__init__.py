from bot.handlers.user_handlers.startup import router as router_startup
from bot.handlers.user_handlers.exchange import router as router_exchange
from bot.handlers.user_handlers.rates import router as router_rates

__all__ = [
    "router_startup",
    "router_exchange",
    "router_rates",
]
