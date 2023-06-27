let sidebar = document.getElementsByClassName("secondsidebar")[0];
let sidebar_content = document.getElementsByClassName("content-wrapper")[0];
      
window.onscroll = () => {
    let scrollTop = window.scrollY;
    let viewportHeight = window.innerHeight;
    let sidebarTop = sidebar.getBoundingClientRect().top + window.pageYOffset;
    let contentHeight = sidebar_content.getBoundingClientRect().height;

    if( scrollTop >= contentHeight - viewportHeight + sidebarTop) {
        sidebar_content.style.transform = `translateY(-${(contentHeight - viewportHeight + sidebarTop)}px)`;
        sidebar_content.style.position  = "fixed"; 
    }
    else{
        sidebar_content.style.transform = "";
        sidebar_content.style.position  = ""; 
        }
};