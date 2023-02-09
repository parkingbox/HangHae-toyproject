// $(document).ready(function () {
//   listing();
// });

function show_content() {
  $.ajax({
    type: "GET",
    url: "https://apis.data.go.kr/B551011/KorService/searchFestival?serviceKey=3WzdkvGaFztwuuD7uF0oPJSKUGEAJWkLJ9PJTYi2ChGhlwpqlsLOuur%2BTg2dkymt6IRTj3QgSlIBa5wDGLNQPg%3D%3D&numOfRows=978&pageNo=1&MobileOS=ETC&MobileApp=AppTest&_type=json&listYN=Y&arrange=C&eventStartDate=20220701",
    data: {},
    success: function (res) {
      const data = res.response.body.items.item;
      // console.log(res.response.body.items.item[0]);
    },
  });
}

function save_data() {
  let data = [];
  $.ajax({
    type: "GET",
    url: "https://apis.data.go.kr/B551011/KorService/searchFestival?serviceKey=3WzdkvGaFztwuuD7uF0oPJSKUGEAJWkLJ9PJTYi2ChGhlwpqlsLOuur%2BTg2dkymt6IRTj3QgSlIBa5wDGLNQPg%3D%3D&numOfRows=978&pageNo=1&MobileOS=ETC&MobileApp=AppTest&_type=json&listYN=Y&arrange=C&eventStartDate=20220701",
    data: {},
    success: function (res) {
      data = res.response.body.items.item;
      // console.log(data);
      // console.log(res.response.body.items.item[0]);
    },
  });

  setTimeout(() => {
    // console.log("$$", data)
    $.ajax({
      type: "POST",
      // contentType: 'application/json',
      dataType: "json",
      // data: JSON.stringify(data),
      data: {
        data: JSON.stringify(data),
      },
      // traditional: true,
      url: "/savedata",
      success: function (res) {
        alert(res["msg"]);
      },
    });
  }, 1000);
}


function get_data(param) {
  console.log(param);
  let data = [];
  // var param = 1556203;
  $.ajax({
    type: "POST",
    url: "/detail/" + param,
    data: {},
    success: function (res) {
      console.log(res.data);
      data = res.data;
      let addr1 = data.addr1;
      let addr2 = data.addr2;
      let eventstartdate = data.eventstartdate;
      let eventenddate = data.eventenddate;
      let firstimage = data.firstimage;
      let firstimage2 = data.firstimage2;
      let mapx = data.mapx;
      let mapy = data.mapy;
      // let modifiedtime = data.modifiedtime;
      let tel = data.tel;
      let title = data.title;

      let info_html = `<ul>
          <li class="title">${title}</li>
          <li class="date">${eventstartdate} ~ ${eventenddate}</li>
          <li class="addr1">📍 : ${addr1}</li>
          <li class="addr2">${addr2}</li>
          <li class="tel">📞 : ${tel}</li>
        </ul>`;
      $(".info_data").append(info_html);

      let poster_html = `<img src="${firstimage}" alt="poster">`;
      $(".poster").append(poster_html);

      var container = document.getElementById("map");
      var options = {
        center: new kakao.maps.LatLng(mapy, mapx),
        level: 3,
      };

      var map = new kakao.maps.Map(container, options);

      // 마커가 표시될 위치입니다
      var markerPosition = new kakao.maps.LatLng(mapy, mapx);

      // 마커를 생성합니다
      var marker = new kakao.maps.Marker({
        position: markerPosition,
      });

      // 마커가 지도 위에 표시되도록 설정합니다
      marker.setMap(map);
    },
  });
}

function login() {
  let id = $("#id").val();
  let pw = $("#pw").val();

  $.ajax({
    type: "POST",
    url: "/login",
    data: {
      id: id,
      pw: pw,
    },
    success: function (response) {
      alert(response["msg"]);
      window.location.reload();
    },
  });
}
