document.addEventListener("DOMContentLoaded", () => {
    const sections = document.querySelectorAll(".menu-section");
    const navLinks = document.querySelectorAll(".nav-list a");
    const navContainer = document.querySelector(".category-nav");

    // Smooth Scrolling when clicking on nav links
    navLinks.forEach(link => {
        link.addEventListener("click", function(e) {
            e.preventDefault();
            const targetId = this.getAttribute("href").substring(1);
            const targetSection = document.getElementById(targetId);
            
            if(targetSection) {
                const navHeight = document.querySelector(".category-nav").offsetHeight;
                window.scrollTo({
                    top: targetSection.offsetTop - navHeight,
                    behavior: "smooth"
                });
            }
        });
    });

    // ScrollSpy to highlight the active menu item and scroll horizontal nav
    window.addEventListener("scroll", () => {
        let current = "";
        
        sections.forEach(section => {
            const sectionTop = section.offsetTop;
            const navHeight = document.querySelector(".category-nav").offsetHeight;
            if (scrollY >= (sectionTop - navHeight - 10)) {
                current = section.getAttribute("id");
            }
        });

        navLinks.forEach(link => {
            link.classList.remove("active");
            if (link.getAttribute("href").substring(1) === current) {
                link.classList.add("active");
                // Auto scroll horizontal nav to keep active item in view
                const linkRect = link.getBoundingClientRect();
                const containerRect = navContainer.getBoundingClientRect();
                
                if(linkRect.left < containerRect.left || linkRect.right > containerRect.right) {
                    navContainer.scrollBy({
                        left: linkRect.left - containerRect.left - 20,
                        behavior: 'smooth'
                    });
                }
            }
        });
    });
});
