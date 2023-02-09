$(document).ready(function () {
  listing();
});

function listing() {
  $.ajax({
    type: "GET",
    url: "/list",
    data: {},
    success: function (res) {
      console.log(res);
      list = res["list"];
      for (let i = 0; i < list.length; i++) {
        let contentid = list[i]["contentid"];
        let img = list[i]["firstimage"];
        let title = list[i]["title"];
        let temp_html = `<a href="/detail/${contentid}" class="col">
                            <div class="card h-100">
                                <img src="${img}"
                                class="card-img-top">
                              <div class="card-body">
                                <h5 class="card-title">${title}</h5>
                              </div>
                            </div>
                          </a>`;
        $("#card-box").append(temp_html);
      }
    },
  });
}
