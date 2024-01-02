from models import Event, Reservation, Craft
from app import db
from datetime import datetime

def check_event_conflict(new_event):
    """ Check for any conflicts with the given event. """
    conflicting_events = Event.query.filter(
        (Event.start_date <= new_event.end_date) & (Event.end_date >= new_event.start_date)
    ).all()

    return bool(conflicting_events)

def create_event(title, description, start_date, end_date, color, location=None):
    """ Create a new event. """
    new_event = Event(title=title, description=description, start_date=start_date, end_date=end_date, color=color, location=location)
    
    if not check_event_conflict(new_event):
        db.session.add(new_event)
        db.session.commit()
        return new_event
    else:
        return None

def check_craft_availability(craft_id, start_time, end_time):
    """ Check if the craft is available in the given time range. """
    overlapping_reservations = Reservation.query.filter(
        Reservation.craft_id == craft_id,
        (Reservation.start_datetime < end_time) & (Reservation.end_datetime > start_time)
    ).all()

    craft = Craft.query.get(craft_id)
    if craft and overlapping_reservations.count() < craft.current_availability:
        return True
    return False

def create_reservation(craft_id, customer_id, start_time, end_time):
    """ Create a new reservation for a craft. """
    if check_craft_availability(craft_id, start_time, end_time):
        new_reservation = Reservation(craft_id=craft_id, customer_id=customer_id, start_datetime=start_time, end_datetime=end_time)
        db.session.add(new_reservation)
        db.session.commit()
        return new_reservation
    else:
        return None

def update_craft_availability(craft_id, delta):
    """ Update the availability of a craft. """
    craft = Craft.query.get(craft_id)
    if craft:
        craft.current_availability += delta
        db.session.commit()

def cancel_reservation(reservation_id):
    """ Cancel a reservation and update craft availability. """
    reservation = Reservation.query.get(reservation_id)
    if reservation:
        update_craft_availability(reservation.craft_id, 1)
        db.session.delete(reservation)
        db.session.commit()
