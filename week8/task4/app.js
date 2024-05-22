async function sendRequestGoogle() {
  let url = "https://www.google.com/";
  let response = await fetch(url, {
    method: "GET",
  });
  return response.status;
}

async function sendRequestPadax() {
  let url =
    "https://padax.github.io/taipei-day-trip-resources/taipei-attractions-assignment.json";
  let response = await fetch(url, { method: "GET" });
  console.log(response.headers);
}
