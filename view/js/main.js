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
          const err = (errorThrown) ? errorThrown : "Unknown error"
          console.error("Status: " + textStatus)
          console.error("Error: " + err)
      } 
  })
}
function updateContent(data) {
  $('main div.result.box ul').html('')
  console.log(data)
  data.map(({type, url, title, description}) => {
    $('main div.result.box ul').append(`
      <li>
        <img src="${type.logo}"/>
        <a href="${url}">${title}</a>
        ${
          ((description) ? "<p class='description'>" + description + "</p>" : '')
        }
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
  nav(page)
  getIt(request, page)
}
function prevPage() {
  if (page == 0) return
  page--
  nav(page)
  getIt(request, page)
}
function nav(page) {
  $('footer div.navigation span.page').text(page + 1)
}

