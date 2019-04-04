class ApplicationController < ActionController::Base

  protect_from_forgery with: :exception
  private

  def confirm_logged_in
    unless session[:user_id]
      redirect_to(:controller => 'access', :action => 'login')
      return false # halts the before_action
    else
      return true
    end
  end

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
