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

    // 新增按鈕
    mainContent = document.querySelector(".mainContent");
    let btn = document.createElement("button");
    let div = document.createElement("div");
    btn.style.padding = "0.5rem";
    btn.style.display = "flex";
    btn.textContent = "Load More";
    div.style.width = "100%";
    div.style.marginTop = "1rem";
    div.style.display = "flex";
    div.style.justifyContent = "center";
    div.appendChild(btn);
    mainContent.appendChild(div);

    // 監聽按鈕事件
    clickTimes = 0;
    btn.addEventListener("click", (e) => {
      let boxes = document.querySelectorAll(".outerEdge");
      if (data.data.results.length - boxes.length < 10) {
        addBox(data.data.results.length - boxes.length);
      } else {
        addBox(10);
      }
      boxes = document.querySelectorAll(".outerEdge");
      for (let i = 13 + clickTimes * 10; i < boxes.length; i++) {
        stitle = spot[i]["stitle"];
        imgURL = "https" + spot[i]["filelist"].split("https")[1];
        addContent(boxes[i], stitle, imgURL);
        if (i == data.data.results.length - 1) {
          btn.style.display = "none";
        }
      }
      clickTimes++;
    });
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

function addBox(n) {
  let biggerBox =
    '<div class="bigBox bigger">\
    <div class="outerEdge">\
      <img src="./star_icon.png" alt="icon" class="icon" />\
    </div>\
  </div>';
  let bigBox =
    '<div class="bigBox">\
    <div class="outerEdge">\
      <img src="./star_icon.png" alt="icon" class="icon" />\
    </div>\
  </div>';

  buttomPart = document.querySelector(".buttom");
  for (let i = 0; i < n; i++) {
    if (i == 0 || i == 5) {
      buttomPart.insertAdjacentHTML("beforeend", biggerBox);
    } else {
      buttomPart.insertAdjacentHTML("beforeend", bigBox);
    }
  }
}
