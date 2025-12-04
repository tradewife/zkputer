from x10.perpetual.orders import OrderTriggerPriceType, OrderPriceType

print("OrderTriggerPriceType members:")
for name, member in OrderTriggerPriceType.__members__.items():
    print(f"  {name}: {member}")

print("\nOrderPriceType members:")
for name, member in OrderPriceType.__members__.items():
    print(f"  {name}: {member}")
