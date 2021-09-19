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
