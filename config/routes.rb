Rails.application.routes.draw do

  root "home#index"
  match ':controller(/:action(/:id))', :via => [:get, :post]

  get 'home/index'
  get 'home/show'
  get 'home/new'
  get 'home/edit'
  get 'access/index'
  get 'access/login'
  get 'access/signup'


  # For details on the DSL available within this file, see http://guides.rubyonrails.org/routing.html
end
