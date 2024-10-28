const contentContainer = document.getElementById("book-content");
let currentPage = 1;
const pageSize = 500; // Character count per page (adjust as necessary)
let totalPages = Math.ceil(contentContainer.innerText.length / pageSize);

// Update page counter display
function updatePageCounter() {
  document.getElementById("current-page").textContent = currentPage;
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

  // Disable buttons at boundaries
  document.getElementById("prev-btn").disabled = page === 1;
  document.getElementById("next-btn").disabled = page === totalPages;

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

// Initialize pagination and set up keyboard navigation
document.addEventListener("DOMContentLoaded", () => {
  // Store the entire book content in a data attribute for easy slicing
  contentContainer.setAttribute(
    "data-full-content",
    contentContainer.innerText
  );

  // Initialize pagination
  totalPages = Math.ceil(contentContainer.innerText.length / pageSize);
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
