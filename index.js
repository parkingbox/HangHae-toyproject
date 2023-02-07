$(function () {
  let y = new Date();
  y.setDate(y.getDate() - 1);
  let str =
    y.getFullYear() +
    "-" +
    ("0" + (y.getMonth() + 1)).slice(-2) +
    "-" +
    ("0" + y.getDate()).slice(-2);
  $("#date").attr("max", str);

  // 버튼 클릭 이벤트
  $("#mybtn").click(function () {
    let d = $("#date").val(); //YYYY-MM-DD
    const regex = /-/g;
    let d_str = d.replace(regex, ""); // YYYYMMDD
    let url =
      "https://apis.data.go.kr/B551011/KorService/searchFestival?serviceKey=3WzdkvGaFztwuuD7uF0oPJSKUGEAJWkLJ9PJTYi2ChGhlwpqlsLOuur%2BTg2dkymt6IRTj3QgSlIBa5wDGLNQPg%3D%3D&numOfRows=10&pageNo=10&MobileOS=ETC&MobileApp=AppTest&_type=json&listYN=Y&arrange=C&eventStartDate=" +
      d_str;

    $.getJSON(url, function (data) {
      let festivalList = data.response.body.items.item;
      $("div").empty();
      for (let i in festivalList) {
        $("div").append(
          "<span>" +
            "<img class='fes__image' src=" +
            festivalList[i].firstimage +
            ">" +
            "<span class='fes__title'>" +
            festivalList[i].title +
            "</span>" +
            "" +
            "</span><br>"
        );
      }
    });
  }); //click
});
