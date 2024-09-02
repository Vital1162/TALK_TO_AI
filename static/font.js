document.addEventListener('DOMContentLoaded', function() {
    // sidebar prob change
    const slider = document.getElementById('temperature');
    const sliderValue = document.getElementById('temp_value');

    const top_p = document.getElementById('top_p')
    const top_pValue = document.getElementById("top_p_value")
    const chatbox = document.getElementById('chatbox');

    slider.addEventListener('input', function() {
        sliderValue.textContent = slider.value;
    });

    top_p.addEventListener('input', ()=>{
        top_pValue.textContent = top_p.value
    })

    function scrollToBottom() {
        chatbox.scrollTop = chatbox.scrollHeight;
    }

    scrollToBottom();

    const observer = new MutationObserver(scrollToBottom);
    observer.observe(chatbox, { childList: true });

    
});


// sidebar adjustment
const sidebar = document.getElementById('sidebar');
const sidebarToggle = document.getElementById('sidebarToggle');
const mediaQuery = window.matchMedia('(max-width: 1400px)');
const content_area = document.getElementById("content_area");
function toggleSidebar() {
    sidebar.classList.toggle('-translate-x-full');
}

function handleWindowResize(e) {
    if (e.matches) {
        sidebar.classList.add('-translate-x-full');

    } else {
        sidebar.classList.remove('-translate-x-full');
    }
}

sidebarToggle.addEventListener('click', toggleSidebar);
mediaQuery.addListener(handleWindowResize);

// Initial check
handleWindowResize(mediaQuery);