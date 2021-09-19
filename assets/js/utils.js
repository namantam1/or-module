function getCookie(name = "csrftoken") {
  let cookieValue = null;
  if (document.cookie && document.cookie !== "") {
    const cookies = document.cookie.split(";");
    for (let i = 0; i < cookies.length; i++) {
      const cookie = cookies[i].trim();
      // Does this cookie string begin with the name we want?
      if (cookie.substring(0, name.length + 1) === name + "=") {
        cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
        break;
      }
    }
  }
  return cookieValue;
}

function setBtnLoading(btn) {
  $(btn).attr("disabled", true);
  $(btn).html(`<span class="spinner-border spinner-border-sm" role="status"
                                aria-hidden="true"></span>`);
}
function unSetBtnLoading(btn, text = "Next") {
  $(btn).removeAttr("disabled");
  $(btn).html(text);
}

function setSpecialization() {
  const department = $("#department").val();

  if (department) {
    $.ajax({
      url: "/specialization/" + department + "/",
      method: "GET",
      success: (res) => {
        if (res) {
          $("#specialization").html(
            res.map((el) => {
              return `<option>${el.value}</option>`;
            })
          );
        }
      },
      error: (err) => {
        console.log(err.responseJSON, err.responseText);
      },
    });
  }
}
