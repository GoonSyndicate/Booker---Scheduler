from app import create_app, db
from models import Craft, Unit, Rate, RateCategory

def add_crafts():
    crafts = [
        Craft(name="24' Bennington SVSR Tritoon", max_availability=7, current_availability=7, reservation_type='Daily'),
        Craft(name='Waverunners', max_availability=5, current_availability=5, reservation_type='Hourly')
    ]
    db.session.add_all(crafts)
    db.session.commit()
    return crafts

def add_units(crafts):
    for craft in crafts:
        craft_prefix = 'benni' if 'Bennington' in craft.name else 'waverunner'
        for i in range(1, craft.max_availability + 1):
            unit_name = f"{craft_prefix} {i}"
            unit = Unit(craft_id=craft.id, name=unit_name)
            db.session.add(unit)
    db.session.commit()

def add_rate_categories():
    categories = ['Per reservation', 'Per 2 hours', 'Per 4 hours', 'Per day', 'Per 6 days']
    for name in categories:
        category = RateCategory(name=name)
        db.session.add(category)
    db.session.commit()
    return RateCategory.query.all()

def add_rates(crafts, categories):
    # Rates are based on the image provided, rounding to the nearest whole number
    tritoon_rates = {'Per reservation': 0, 'Per 4 hours': 325, 'Per day': 475, 'Per 6 days': 2199}
    waverunner_rates = {'Per 2 hours': 225, 'Per 4 hours': 325, 'Per day': 425, 'Per 6 days': 1875}

    # Map category names to the category objects
    category_mapping = {category.name: category for category in categories}

    # Add rates for Bennington Tritoon
    for name, amount in tritoon_rates.items():
        if amount > 0:  # Only add rates that are greater than 0
            rate = Rate(
                category_id=category_mapping[name].id,
                product_id=[craft for craft in crafts if "Bennington" in craft.name][0].id,
                amount=amount
            )
            db.session.add(rate)

    # Add rates for Waverunners
    for name, amount in waverunner_rates.items():
        if amount > 0:  # Only add rates that are greater than 0
            rate = Rate(
                category_id=category_mapping[name].id,
                product_id=[craft for craft in crafts if 'Waverunners' in craft.name][0].id,
                amount=amount
            )
            db.session.add(rate)

    db.session.commit()

if __name__ == '__main__':
    app = create_app()
    with app.app_context():
        crafts = add_crafts()
        categories = add_rate_categories()
        add_rates(crafts, categories)
