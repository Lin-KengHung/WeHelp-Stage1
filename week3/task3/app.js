let url =
  "https://padax.github.io/taipei-day-trip-resources/taipei-attractions-assignment-1";

let spot;

fetch(url)
  .then(function (response) {
    return response.json();
  })
  .then(function (data) {
    // console.log(data.data.results);
    spot = data.data.results;

    let boxes = document.querySelectorAll(".outerEdge");

    for (let i = 0; i < boxes.length; i++) {
      stitle = spot[i]["stitle"];
      imgURL = "https" + spot[i]["filelist"].split("https")[1];
      addContent(boxes[i], stitle, imgURL);
    }
  });

function addContent(box, stitle, imgURL) {
  let img = document.createElement("img");
  let p = document.createElement("p");
  let title = document.createTextNode(stitle);
  img.src = imgURL;
  img.alt = "圖";
  img.className = "main";
  p.style.overflow = "hidden";
  p.style.textOverflow = "ellipsis";
  p.style.whiteSpace = "nowrap";
  p.appendChild(title);
  box.appendChild(img);
  box.appendChild(p);
}
