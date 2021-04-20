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
function addNavTabs() {
  const tab_list_text = [
     {
       name: "Main",
       key: "main"
     }, {
       name: "Social",
       key: "social"
     }
  ]
  const tab_list_image = [
     {
       name: "Look for image",
       key: "main"
     }, {
       name: "Display image",
       key: "social"
     }
  ]
  const block_navigation_tab_text = $('.tab.navigation.search.text ul')
  const block_navigation_tab_image = $('.tab.navigation.search.image ul')
  tab_list_text.forEach(({ name, key }) => block_navigation_tab_text.append("<li key='" + key + "'>" + name + "</li>"))
  tab_list_image.forEach(({ name, key }) => block_navigation_tab_image.append("<li key='" + key + "'>" + name + "</li>"))
}
