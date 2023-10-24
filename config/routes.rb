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
  root "users#index"
end
