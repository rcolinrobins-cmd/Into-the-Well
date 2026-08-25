/**
 * Thin wrapper around Square's REST API — deliberately not using the
 * official `square` npm SDK, so there's no dependency to install and no
 * risk of this code drifting out of sync with whatever SDK major version
 * ends up installed. Square's REST API is calendar-versioned (the
 * Square-Version header below), which is the whole point: pin a version,
 * everything behaves the same until you deliberately bump it.
 * https://developer.squareup.com/reference/square
 */

// Bump this occasionally to pick up new API features — see
// https://developer.squareup.com/docs/square-versions-overview for the
// current release. Payments/refunds on this version stay stable even as
// newer versions ship.
const SQUARE_API_VERSION = "2025-01-23";

function squareBaseUrl() {
  return process.env.SQUARE_ENVIRONMENT === "production"
    ? "https://connect.squareup.com"
    : "https://connect.squareupsandbox.com";
}

/**
 * @param {string} path e.g. "/v2/payments"
 * @param {{method?: string, body?: object}} [options]
 */
async function squareRequest(path, options = {}) {
  const accessToken = process.env.SQUARE_ACCESS_TOKEN;
  if (!accessToken) {
    throw new Error("SQUARE_ACCESS_TOKEN is not set");
  }

  const res = await fetch(squareBaseUrl() + path, {
    method: options.method || "GET",
    headers: {
      "Content-Type": "application/json",
      Authorization: "Bearer " + accessToken,
      "Square-Version": SQUARE_API_VERSION,
    },
    body: options.body ? JSON.stringify(options.body) : undefined,
  });

  const data = await res.json().catch(function () { return {}; });

  if (!res.ok) {
    var detail = data.errors && data.errors[0] && data.errors[0].detail;
    var err = new Error(detail || "Square API request failed (" + res.status + ")");
    err.status = res.status;
    err.squareErrors = data.errors;
    throw err;
  }

  return data;
}

module.exports = { squareRequest, squareBaseUrl, SQUARE_API_VERSION };
