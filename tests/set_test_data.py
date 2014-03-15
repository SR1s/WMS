from WMS.models import Place, Account, Item, Order, OrderDetail

def set_up_data(db):
    # add 4 places
    shenzhen = Place("Shenzhen")
    db.session.add(shenzhen)
    guangzhou = Place("guangzhou")
    db.session.add(guangzhou)
    hongkong = Place("hongkong")
    db.session.add(hongkong)
    shanghai = Place("shanghai")
    db.session.add(shanghai)
    db.session.commit()

    # add 4 users
    a_shenzhen = Account("a_shenzhen", "a_shenzhen", shenzhen.id)
    db.session.add(a_shenzhen)
    a_guangzhou = Account("a_guangzhou", "a_guangzhou", guangzhou.id)
    db.session.add(a_guangzhou)
    a_hongkong = Account("a_hongkong", "a_hongkong", hongkong.id)
    db.session.add(a_hongkong)
    a_shanghai = Account("a_shanghai", "a_shanghai", shanghai.id)
    db.session.add(a_shanghai)
    db.session.commit()

    i1 = Item("G75189", "AFA A SHO", \
              "XS", 0, "S", 2, "M", 2, \
              "L", 1, "XL", 1, "XXL", 0, \
              shenzhen.id)
    i2 = Item("G74569", "AFA F JSY", \
              "XS", 0, "S", 10, "M", 10, \
              "L", 5, "XL", 3, "XXL", 1, \
              guangzhou.id)
    i3 = Item("G75185", "AFA H JSY W", \
              "XS", 10, "S", 10, "M", 5, \
              "L", 1, "XL", 0, "XXL", 0, \
              shanghai.id)

    db.session.add(i1)
    db.session.add(i2)
    db.session.add(i3)
    db.session.commit()

    order = Order("10000")
    db.session.add(order)
    db.session.commit()

    od_1 = OrderDetail("G75187", "S", "AFA A JSY", 4, order.id)
    db.session.add(od_1)
    db.session.commit()