$(document).ready(function () {
  listing();
});

function listing() {
  $.ajax({
    type: "GET",
    url: "/list",
    data: {},
    success: function (res) {
      list = res["list"];
      $("#btn").click(function () {
        
  $("#card-box").empty();
        let date = $("#date").val();
        const regex = /-/g;
        let date_str = date.replace(regex, "");

        for (let i = 0; i < list.length; i++) {
          let eventstartdate = list[i]["eventstartdate"];
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
          if (date_str == eventstartdate) {
            $("#card-box").append(temp_html);
          }
        }
      });
    },
  });
}
