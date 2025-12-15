

const LIST_OF_PAGES = ["Sacramento", "Los Angeles", "San Diego", "Contact Us"];

// populates navbar to other pages on website
function populateNavbar() {
    // get nav block
    const navblock = document.getElementsByTagName("nav")[0];
    // create a UL for the hyperlinks
    const navbar = document.createElement("ul");

    // create link to home page
    const nav_item = document.createElement("li");
    const home_nav = document.createElement("a");
    home_nav.innerHTML = "Home";
    home_nav.href = "index.html";
    nav_item.appendChild(home_nav);
    navbar.appendChild(nav_item);

    // for each page in our list, add link to navbar
    for (let n in LIST_OF_PAGES) {
        const page_name = LIST_OF_PAGES[n]
        
        // don't create a link to the current page
        if (document.title.includes(page_name)) continue;

        // add link to nav bar
        const nav_item = document.createElement("li");
        const nav_element = document.createElement("a");
        nav_element.innerHTML = page_name;
        nav_element.href = page_name+".html";
        nav_item.appendChild(nav_element)
        navbar.appendChild(nav_item);
    }
    // add list of hyperlinks to nav block
    navblock.appendChild(navbar);
}

window.onload = function() {

    // populates vertical navbar when DOM elements have loaded for webpages that have one (all except home page)
    if (!document.title.includes("The State of California")) populateNavbar();
    
    // checks if the contact form exists, then adds event listener for submision if it does
    let conatct_form = document.querySelector("#contact-form");
    if (conatct_form) {
        conatct_form.addEventListener("submit", (event) => {
            let email_input   = document.querySelector("#email-input");
            let email_confirm = document.querySelector("#email-confirm");

            // if email addresses don't match, alert and cancel submission 
            if (email_input.value != email_confirm.value) {
                alert("Email addresses do not match");
                event.preventDefault();
            }
            
        });
    }

}


