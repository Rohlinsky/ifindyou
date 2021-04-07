function searchRun() {
  $('div.look').click(() => {
    setRequest()
    getIt(request)
  })
}
function setRequest() {
  request = $('input.request').val()
  if (request === '') throw new Error("Request must be full")
}
function keyboard() {
  document.onkeydown = ({keyCode}) => {
    switch (keyCode) {
      case 13:
        setRequest()
        getIt(request)
        break
      case 37:
        prevPage()
        break
      case 39:
        nextPage()
        break
      default:
        return
    }
  };
}
function getIt(lookIt, page_number=0) {
  $.ajax({
      beforeSend: () => console.log("Process start"),
      type: "GET",  
      url: "/look/" + lookIt + "/page/" + page_number,
      success: (data) => {
        updateContent(data)
        if (!inited) {
          initNavigation()
          inited = 1
        }
      },
      error: (XMLHttpRequest, textStatus, errorThrown) => { 
          alert("Status: " + textStatus); alert("Error: " + errorThrown); 
      } 
  })
}
function updateContent(data) {
  $('main div.result.box ul').html('')
  data.map(function (item) {
    $('main div.result.box ul').append(`
      <li>
        <img src="${item.type.logo}"/>
        <a href="${item.url}">${item.text}</a>
      </li>
    `)
  })
}
function initNavigation() {
  $('footer div.navigation div.btn-success.next').click(() => {
    nextPage()
  })
  $('footer div.navigation div.btn-success.prev').click(() => {
    prevPage()
  })
}
function nextPage() {
  page++
  getIt(request, page)
}
function prevPage() {
  if (page == 0) return
  page--
  getIt(request, page)
}
