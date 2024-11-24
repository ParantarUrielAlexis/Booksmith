const contentContainer = document.getElementById("book-content");
const pageInput = document.getElementById("page-input");
const prevButton = document.getElementById("prev-btn");
const nextButton = document.getElementById("next-btn");

let currentPage = parseInt(localStorage.getItem("currentPage"), 10) || 1; // Restore saved page or default to 1
const pageSize = 700; // Characters per page
let totalPages;

// Update page counter display
function updatePageCounter() {
  pageInput.value = currentPage; // Update the input field
  document.getElementById("total-pages").textContent = totalPages;
}

// Paginate content and display the specified page
function showPage(page) {
  // Calculate start and end indices
  const start = (page - 1) * pageSize;
  const end = page * pageSize;

  // Slice the text content and display the required section
  contentContainer.innerText = contentContainer
    .getAttribute("data-full-content")
    .slice(start, end);

  // Save the current page to localStorage
  localStorage.setItem("currentPage", currentPage);

  // Disable buttons at boundaries
  prevButton.disabled = page === 1;
  nextButton.disabled = page === totalPages;

  updatePageCounter();
}

// Navigate to the next page
function nextPage() {
  if (currentPage < totalPages) {
    currentPage++;
    showPage(currentPage);
  }
}

// Navigate to the previous page
function prevPage() {
  if (currentPage > 1) {
    currentPage--;
    showPage(currentPage);
  }
}

// Jump to a specific page via input
function jumpToPage() {
  const inputPage = parseInt(pageInput.value, 10);

  if (inputPage >= 1 && inputPage <= totalPages) {
    currentPage = inputPage;
    showPage(currentPage);
  } else {
    alert(
      `Invalid page number. Please enter a number between 1 and ${totalPages}.`
    );
    pageInput.value = currentPage; // Reset input to the current page
  }
}

// Initialize pagination and set up keyboard navigation
document.addEventListener("DOMContentLoaded", () => {
  // Store the entire book content in a data attribute for easy slicing
  contentContainer.setAttribute(
    "data-full-content",
    contentContainer.innerText
  );

  // Calculate total pages
  totalPages = Math.ceil(contentContainer.innerText.length / pageSize);

  // Display the saved or default page
  showPage(currentPage);

  // Add keyboard navigation
  document.addEventListener("keydown", (event) => {
    if (event.key === "ArrowRight") {
      nextPage();
    } else if (event.key === "ArrowLeft") {
      prevPage();
    }
  });
});
