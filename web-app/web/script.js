fetch("https://your-api-id.execute-api.region.amazonaws.com/prod/") 
 //change this ^^^^^^
  .then(res => res.json())
  .then(data => {
    document.getElementById("wait-time").innerText = `Wait time: ${data.wait_time} minutes`;
  });
