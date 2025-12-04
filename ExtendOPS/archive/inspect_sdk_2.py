import inspect
from x10.perpetual.trading_client import PerpetualTradingClient
from x10.perpetual.orders import OrderTpslType
from x10.perpetual.order_object import OrderTpslTriggerParam

print("OrderTpslType members:")
for name, member in OrderTpslType.__members__.items():
    print(f"  {name}: {member}")

print("\nOrderTpslTriggerParam signature:")
print(inspect.signature(OrderTpslTriggerParam))

print("\nPerpetualTradingClient methods:")
methods = inspect.getmembers(PerpetualTradingClient, predicate=inspect.isfunction)
for name, func in methods:
    if "order" in name:
        print(f"  {name}")
