Rails.application.routes.draw do
  devise_for :users
  # Define your application routes per the DSL in https://guides.rubyonrails.org/routing.html

  # Defines the root path route ("/")
  # root "articles#index"
  resources :users do
    # request type is via
    # collection is so that it can be /users/scrape shallow nesting
    match '/scrape', to: 'users#scrape', via: :post, on: :collection
  end
  resources :players, :volunteers

  get 'ayso', to: 'scrappers#sports_connect_enrollment_details'
  #get '', to: 'scrappers#' Admin Credentials
  #get '', to: 'scrappers#' Coach and Refere Lisence
  get 'update', to: "scrappers#csv_database_volunteer"
  get 'selenium_test', to: 'scrappers#universal_scrape'

  root "users#index"
end
