document.getElementById("download-btn").addEventListener("click", function () {
  const card = document.getElementById("capture-card");

  html2canvas(card, { backgroundColor: "#ffffff", scale: 2 }).then(function (canvas) {
    const link = document.createElement("a");
    link.download = "sentiment_result.png";
    link.href = canvas.toDataURL("image/png");
    link.click();
  });
});