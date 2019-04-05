class ApplicationController < ActionController::Base

  # protects from forgery
  protect_from_forgery with: :exception
  private

  # checks if a user has logged in before they can move to a particular page
  # if not logged in, redirects to login page
  def confirm_logged_in
    unless session[:user_id]
      redirect_to(:controller => 'access', :action => 'login')
      return false # halts the before_action
    else
      return true
    end
  end

  # checks if a logged in user is banned before they can move to a particular page
  # if banned, redirect to user profile page
  def confirm_not_banned
    if session[:user_id]
      @user = User.find(session[:user_id])
      if @user.ban_date != nil
        redirect_to(:controller => 'access', :action => 'index')
        return false # halts the before_action
      else
        return true
      end
    else
      return true
    end
  end

end
