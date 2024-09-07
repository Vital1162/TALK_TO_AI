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

    
    // sidebar and history adjustment
    const history = document.getElementById("chat_history");


    const sidebar = document.getElementById('sidebar');
    const sidebarToggle = document.getElementById('sidebarToggle');
    const mediaQuery = window.matchMedia('(max-width: 1400px)');

    function toggleSidebar() {
        sidebar.classList.toggle('-translate-x-full');

    }

    function handleWindowResize(e) {

        if (e.matches) {
            history.classList.add('translate-x-full');
            sidebar.classList.add('-translate-x-full');
        } else {
            history.classList.remove('translate-x-full');
            sidebar.classList.remove('-translate-x-full');
        }
    }

    sidebarToggle.addEventListener('click', toggleSidebar);
    mediaQuery.addListener(handleWindowResize);

    // Initial check
    handleWindowResize(mediaQuery);

    

    const reset = document.getElementById("reset");
    reset.addEventListener("click", ()=>{
        
        
        
        document.getElementById("config").reset();
        // changing span value this just for show
        sliderValue.textContent = "0.5"
        top_pValue.textContent = "0.9"
        

    })
    const new_conversation = document.getElementById("new_conversation");
    new_conversation.addEventListener("click", ()=>{
        
        console.log("reset page")
        
        window.location.reload()

    })
});


