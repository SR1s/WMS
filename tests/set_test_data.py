from WMS.models import Place, Account, Item, Order, OrderDetail, Storage

def set_up_data(db):
    # add 4 places
    shenzhen = Place(place='Shenzhen')
    db.session.add(shenzhen)
    guangzhou = Place(place='guangzhou')
    db.session.add(guangzhou)
    hongkong = Place(place='hongkong')
    db.session.add(hongkong)
    shanghai = Place(place='shanghai')
    db.session.add(shanghai)
    db.session.commit()

    # add 4 users
    a_shenzhen = Account(user_no ='a_shenzhen', user_ps='a_shenzhen', \
                         place_id=shenzhen.id)
    db.session.add(a_shenzhen)
    a_guangzhou = Account(user_no ='a_guangzhou', user_ps='a_guangzhou', \
                          place_id=guangzhou.id)
    db.session.add(a_guangzhou)
    a_hongkong = Account(user_no ='a_hongkong', user_ps='a_hongkong', \
                         place_id=hongkong.id)
    db.session.add(a_hongkong)
    a_shanghai = Account(user_no ='a_shanghai', user_ps='a_shanghai', \
                         place_id=shanghai.id)
    db.session.add(a_shanghai)
    db.session.commit()

    # add 4 item
    i1 = Item(number="G75189", description="AFA A SHO")
    db.session.add(i1)
    i2 = Item(number="G74569", description="AFA F JSY")
    db.session.add(i2)
    i3 = Item(number="G75185", description="AFA H JSY W")
    db.session.add(i3)
    i4 = Item(number="G75188", description="AFA H JSY W GG")
    db.session.add(i4)
    db.session.commit()

    # add storage
    s1 = Storage(size='XS', amount=10,item_id=i1.id, place_id=shenzhen.id)
    s2 = Storage(size='S', amount=10,item_id=i1.id, place_id=shenzhen.id)
    s3 = Storage(size='M', amount=10,item_id=i1.id, place_id=shenzhen.id)
    s4 = Storage(size='L', amount=10,item_id=i1.id, place_id=shenzhen.id)
    s5 = Storage(size='XL', amount=10,item_id=i1.id, place_id=shenzhen.id)
    s6 = Storage(size='XXL', amount=10,item_id=i1.id, place_id=shenzhen.id)
    db.session.add(s1)
    db.session.add(s2)
    db.session.add(s3)
    db.session.add(s4)
    db.session.add(s5)
    db.session.add(s6)
    db.session.commit()