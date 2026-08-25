/**
 * GET /api/config — public, non-secret configuration for the browser.
 *
 * Square's applicationId and locationId are explicitly documented as safe
 * to expose client-side (they're required to initialize the Web Payments
 * SDK in the browser) — the secret is SQUARE_ACCESS_TOKEN, which never
 * leaves this /api directory. See js/checkout.js for how this is used.
 */
module.exports = function handler(req, res) {
  if (req.method !== "GET") {
    res.setHeader("Allow", "GET");
    return res.status(405).json({ error: "Method not allowed" });
  }

  var applicationId = process.env.SQUARE_APPLICATION_ID;
  var locationId = process.env.SQUARE_LOCATION_ID;
  var environment = process.env.SQUARE_ENVIRONMENT === "production" ? "production" : "sandbox";
  var bookingUrl = process.env.SQUARE_BOOKING_URL || null;

  if (!applicationId || !locationId) {
    // Tell the client plainly that payments aren't configured yet, rather
    // than returning a half-filled config that fails confusingly deeper
    // inside the Square SDK.
    return res.status(200).json({ configured: false, environment: environment, bookingUrl: bookingUrl });
  }

  return res.status(200).json({
    configured: true,
    applicationId: applicationId,
    locationId: locationId,
    environment: environment,
    bookingUrl: bookingUrl,
  });
};
