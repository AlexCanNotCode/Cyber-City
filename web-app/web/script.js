async function fetchWaitTime() {
  const guestId = document.getElementById("guestIdInput").value.trim();
  const output = document.getElementById("output");
  const resultCard = document.getElementById("result");
  const loading = document.getElementById("loading");

  if (!guestId) {
    alert("Please enter your Guest ID.");
    return;
  }

  resultCard.classList.remove("hidden");
  loading.classList.remove("hidden");
  output.classList.add("hidden");
  output.textContent = "";

  try {
    const response = await fetch("https://your-api-id.execute-api.us-east-1.amazonaws.com", {
      method: "POST",
      headers: {
        "Content-Type": "application/json"
      },
      body: JSON.stringify({ guestId })
    });

    if (!response.ok) throw new Error("API error");

    const data = await response.json();

    output.textContent = `🎡 Recommended Ride: ${data.ride} — ⏳ Wait Time: ${data.waitTime}`;
  } catch (error) {
    output.textContent = "⚠️ Unable to fetch wait time. Please try again later.";
  } finally {
    loading.classList.add("hidden");
    output.classList.remove("hidden");
  }
}
