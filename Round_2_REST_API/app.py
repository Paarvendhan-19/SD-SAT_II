from flask import Flask, request, jsonify

app = Flask(__name__)
events = [{"id": 201, "name": "Concert"}]
seats = {15: "Available"}
bookings = {}


@app.get("/api/events")
def search_events():
    name = request.args.get("name", "").lower()
    return jsonify([e for e in events if name in e["name"].lower()])


@app.get("/api/events/<int:event_id>/seats")
def get_seats(event_id):
    return jsonify(seats)


@app.post("/api/bookings")
def reserve_seat():
    data = request.get_json()
    seat_id = data["seatId"]
    if seats.get(seat_id) != "Available":
        return jsonify({"error": "Seat unavailable"}), 409

    booking_id = len(bookings) + 501
    bookings[booking_id] = {
        "bookingId": booking_id,
        "seatId": seat_id,
        "status": "Reserved"
    }
    seats[seat_id] = "Reserved"
    return jsonify(bookings[booking_id]), 201


@app.get("/api/bookings/<int:booking_id>")
def get_booking(booking_id):
    if booking_id not in bookings:
        return jsonify({"error": "Booking not found"}), 404
    return jsonify(bookings[booking_id])


@app.delete("/api/bookings/<int:booking_id>")
def cancel_booking(booking_id):
    if booking_id not in bookings:
        return jsonify({"error": "Booking not found"}), 404
    seat_id = bookings[booking_id]["seatId"]
    seats[seat_id] = "Available"
    bookings[booking_id]["status"] = "Cancelled"
    return jsonify(bookings[booking_id])


if __name__ == "__main__":
    app.run(debug=True)
