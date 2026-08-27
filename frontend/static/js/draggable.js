(function() {
    const chatWindow = document.getElementById('chat-window');
    const chatHeader = document.getElementById('chat-header');

    let isDragging = false;
    let currentX;
    let currentY;
    let initialX;
    let initialY;
    let xOffset = 0;
    let yOffset = 0;

    chatWindow.addEventListener('mousedown', dragStart);
    document.addEventListener('mousemove', drag);
    document.addEventListener('mouseup', dragEnd);

    function dragStart(e) {
        // Exclude interactive elements from triggering drag
        const ignoreElements = ['BUTTON', 'INPUT', 'SELECT', 'TEXTAREA', 'I'];
        if (ignoreElements.includes(e.target.tagName)) return;
        
        initialX = e.clientX - xOffset;
        initialY = e.clientY - yOffset;

        if (e.target === chatWindow || chatWindow.contains(e.target)) {
            isDragging = true;
            chatWindow.style.transition = 'none'; // Disable transition while dragging
        }
    }

    function drag(e) {
        if (isDragging) {
            e.preventDefault();
            currentX = e.clientX - initialX;
            currentY = e.clientY - initialY;

            xOffset = currentX;
            yOffset = currentY;

            setTranslate(currentX, currentY, chatWindow);
        }
    }

    function setTranslate(xPos, yPos, el) {
        el.style.transform = `translate3d(${xPos}px, ${yPos}px, 0)`;
    }

    function dragEnd(e) {
        initialX = currentX;
        initialY = currentY;
        isDragging = false;
        chatWindow.style.transition = ''; // Restore transition
    }
})();
