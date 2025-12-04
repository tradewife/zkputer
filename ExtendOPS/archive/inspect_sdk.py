import inspect
from x10.perpetual.trading_client import PerpetualTradingClient
from x10.perpetual.orders import OrderType
from x10.perpetual.order_object import OrderTpslTriggerParam

print("OrderType members:")
for name, member in OrderType.__members__.items():
    print(f"  {name}: {member}")

print("\nPerpetualTradingClient.place_order signature:")
sig = inspect.signature(PerpetualTradingClient.place_order)
print(sig)

print("\nOrderTpslTriggerParam signature:")
print(inspect.signature(OrderTpslTriggerParam))
