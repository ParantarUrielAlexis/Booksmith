<!-- BACK TO TOP LINK -->

<a id="readme-top"></a>

<!-- PROJECT SHIELDS -->
<!-- Using markdown "reference style" links for readability. -->

<!-- PROJECT LOGO -->
<br />
<div align="center">
  <a href="https://github.com/your_username/booksmith">
    <img src="booksmith_proj\static\images\booksmith_logo.png" alt="BookSmith Logo" width="80" height="80">
  </a>
  <h3 align="center">BookSmith</h3>
  <p align="center">
    A platform where users pay to access and review a wide range of books! <br />
    <a href="https://docs.google.com/document/d/10Cw3C3ilcSdRM_LInJp07nwLXJp7G9ItukQ31gas7rg/edit?usp=sharingh"><strong>Documentary</strong></a>
  </p>
</div>

<!-- TABLE OF CONTENTS -->
<details>
  <summary><strong>Table of Contents</strong></summary>
  <ol>
    <li><a href="#about-the-project">About The Project</a></li>
    <li><a href="#features">Features</a></li>
    <li><a href="#built-with">Built With</a></li>
    <li><a href="#getting-started">Getting Started</a></li>
    <li><a href="#usage">Usage</a></li>
    <li><a href="#roadmap">Roadmap</a></li>
    <li><a href="#contributing">Contributing</a></li>
    <li><a href="#license">License</a></li>
    <li><a href="#contact">Contact</a></li>
    <li><a href="#acknowledgments">Acknowledgments</a></li>
  </ol>
</details>

<!-- ABOUT THE PROJECT -->

## About The Project

**BookSmith** is a comprehensive platform that brings book enthusiasts together, offering an extensive library of books, review functionalities, and personalized recommendations. The platform is designed to cater to a wide audience with diverse reading preferences, ensuring an intuitive and seamless user experience.

### Why BookSmith?

- **Diverse Book Collection**: Access a wide range of books spanning various genres, catering to different interests—from fiction to non-fiction, academic to leisure reading.
- **Community-Driven Reviews**: Users can write and share their own reviews, as well as read reviews from other readers, creating an interactive book-loving community.
- **Secure Payment Integration**: A robust and secure payment system allows users to purchase premium content with confidence.
- **User-Centric Design**: BookSmith is built with a user-friendly interface that is easy to navigate, ensuring readers can find, review, and purchase books with minimal effort.
- **Supports Diverse Learning Styles**: Tailored for users who have different reading preferences, with personalized recommendations and easy access to user-generated content.

<p align="right">(<a href="#readme-top">back to top</a>)</p>

## Features

- **User Profiles**:

  - Users can create and manage personal profiles.
  - Includes customizable profile images, detailed bios, and a list of purchased books.
  - Ability to update personal details and manage preferences.

- **Book Reviews**:

  - Read, write, and reply to book reviews.
  - Users can rate books and share their thoughts.
  - Reply feature allows for engaging discussions about books.
  - Dynamic display of profile images in the review section based on who posted the review.

- **Cart Management**:

  - Easily add, update, or remove books from the shopping cart.
  - Real-time cart updates to reflect changes instantly.
  - Visual indicators for items added or removed from the cart.

- **Personalized Recommendations**:

  - Intelligent book suggestions based on user preferences and past purchases.
  - Tailored recommendations to match unique reading interests.
  - Ability to explore similar books or genres based on reading history.

- **Responsive Design**:
  - Fully optimized for various devices including desktops, tablets, and smartphones.
  - Adaptive layout for a seamless experience on any screen size.
  - Consistent and user-friendly interface for both mobile and desktop views.

<p align="right">(<a href="#readme-top">back to top</a>)</p>

 <!-- BUILT WITH -->

## Built-With

- ![Django](https://img.shields.io/badge/Django-092E20?style=for-the-badge&logo=django&logoColor=white)
- ![SQLite](https://img.shields.io/badge/SQLite-07405E?style=for-the-badge&logo=sqlite&logoColor=white)
- ![HTML5](https://img.shields.io/badge/HTML5-E34F26?style=for-the-badge&logo=html5&logoColor=white)
- ![CSS3](https://img.shields.io/badge/CSS3-1572B6?style=for-the-badge&logo=css3&logoColor=white)
- ![Bootstrap](https://img.shields.io/badge/Bootstrap-563D7C?style=for-the-badge&logo=bootstrap&logoColor=white)
- ![JavaScript](https://img.shields.io/badge/JavaScript-F7DF1E?style=for-the-badge&logo=javascript&logoColor=black)
- ![jQuery](https://img.shields.io/badge/jQuery-0769AD?style=for-the-badge&logo=jquery&logoColor=white)
- ![SweetAlert](https://img.shields.io/badge/SweetAlert2-FF4154?style=for-the-badge&logo=sweetalert&logoColor=white)
- ![Font Awesome](https://img.shields.io/badge/Font%20Awesome-339AF0?style=for-the-badge&logo=fontawesome&logoColor=white)
- ![TTK Bootstrap](https://img.shields.io/badge/TTK%20Bootstrap-7952B3?style=for-the-badge&logo=bootstrap&logoColor=white)

## Getting Started

To get a local copy of the BookSmith project up and running, follow these simple steps.

### Prerequisites

Before you begin, ensure you have the following software installed:

- **Python 3.x** or later
- **Django** for back-end development
- **Pip** for installing Python dependencies

Install **Django** and **other dependencies**:

```sh
pip install django
```

### Installation

1. Clone the repository
   ```sh
   git clone https://github.com/your_username/booksmith.git
   ```
2. Install the required dependencies

   ```sh
   pip install -r requirements.txt

   ```

3. Change Directory
   ```sh
   cd booksmith_proj
   ```
4. Set up the database
   ```sh
   python manage.py migrate
   ```
5. Create a superuser (optional for admin access)
   ```sh
   python manage.py createsuperuser
   ```
6. Run the development server
   ```sh
   python manage.py runserver
   ```

### Roadmap

The BookSmith platform is continuously evolving. Below is the roadmap of planned features and improvements:

1. **Quarter 4 2024**:

   - Add support for **multiple languages** for international users.
   - Integrate **social media login** (Google, Facebook).
   - Improve **personalized book recommendations** using machine learning.

2. **Quarter 1 2025**:

   - **Mobile app development** for iOS and Android.
   - Implement a **subscription model** for exclusive book access.
   - Introduce **author profiles** to allow authors to interact with readers.

3. **Quarter 2 2025**:

   - Enhance **review system** with voting (upvote/downvote).
   - Add **audiobook support** to allow users to listen to their favorite books.
   - Introduce **book clubs** where users can join and participate in discussions.

4. **Future**:
   - Expand the **payment system** to support multiple currencies.
   - Add a **community forum** for users to discuss books and share recommendations.
   - Implement **offline reading** for users to access books without an internet connection.

We welcome feedback and contributions. If you have any ideas or suggestions, please feel free to contribute or open an issue.

## Contributing

Contributions are what make the open source community such an amazing place to learn, inspire, and create. Any contributions you make are **greatly appreciated**.

If you have a suggestion that would make this better, please fork the repo and create a pull request. You can also simply open an issue with the tag "enhancement".
Don't forget to give the project a star! Thanks again!

### Steps to Contribute:

1. **Fork the Project**  
   Click the "Fork" button at the top of the repo.

2. **Create a Feature Branch**
   ```sh
   git checkout -b feature/AmazingFeature
   ```

## Top Contributors:

[![Contributor 1](https://contrib.rocks/image?repo=ParantarUrielAlexis/Booksmith)](https://github.com/ParantarUrielAlexis/Booksmith/graphs/contributors)

## Contact

For any questions, feel free to reach out!

- **Project Link**: [https://github.com/ParantarUrielAlexis/Booksmith](https://github.com/ParantarUrielAlexis/Booksmith)
- **Email**: https.booksmith@gmail.com

Thank you for checking out BookSmith!

## Acknowledgements

We would like to express our gratitude to the following resources and people who made BookSmith possible:

- **[Django](https://www.djangoproject.com/)**: The back-end framework that powers the project.
- **[Bootstrap](https://getbootstrap.com/)**: For providing the responsive and customizable front-end framework.
- **[Font Awesome](https://fontawesome.com/)**: For offering free and high-quality icons.
- **[React](https://reactjs.org/)**: For enhancing the user experience with interactive elements (if applicable).
- **[Pillow](https://pillow.readthedocs.io/en/stable/)**: For image handling in the application.
- **[SweetAlert2](https://sweetalert2.github.io/)**: For beautiful and customizable pop-up alerts.
- **[OpenAI](https://openai.com/)**: For AI-powered features and integration (if applicable).
- **[Contrib.rocks](https://contrib.rocks/)**: For tracking top contributors to the project.

Special thanks to all contributors who have helped improve this project!
