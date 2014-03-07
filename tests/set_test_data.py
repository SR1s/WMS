from WMS.models import Place, Account

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