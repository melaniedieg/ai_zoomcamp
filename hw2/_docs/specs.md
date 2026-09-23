# TableTurn — product specification

## Goal

Help a small restaurant host track walk-in parties and seat them in order. The host needs a shared, persistent queue that survives a page refresh and server restart.

## Users and stories

- As a host, I can add a party with a name and a party size from 1 to 20 so I can track who is waiting.
- As a host, I can see waiting parties in arrival order, including their wait time, so I know who arrived first.
- As a host, I can mark a party seated or remove a party that left. Both actions remove it from the active queue.
- As a host, I can view the day's seated and removed parties to audit changes.

## Acceptance criteria

1. An empty or whitespace-only name, a name longer than 80 characters, and a size outside 1–20 are rejected without changing the queue.
2. Adding a valid party shows it at the bottom of the waiting queue immediately.
3. Clicking Seat or Remove updates the party status and the visible queue immediately.
4. Reloading the page or restarting the backend retains all parties and their statuses in SQLite.
5. The frontend calls the backend through the documented `/api/parties` endpoints; the API schema is in `openapi.yaml`.

## Non-goals

No guest accounts, SMS notifications, table allocation, reservations, multiple restaurants, or automatic estimates. This is a local single-host prototype; simultaneous hosts may need an explicit refresh to see one another's changes.
