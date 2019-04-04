class AccessController < ApplicationController
  before_action :confirm_logged_in, :except => [:login, :attempt_login, :logout, :signup, :attempt_signup]
  before_action :confirm_not_banned, :except => [:index, :login, :attempt_login, :logout, :signup, :attempt_signup]

  def index
    @user = User.find(session[:user_id])
    @banned = false
    if @user.ban_date != nil
      if Date.today - 7.days > @user.ban_date
        @user.ban_date = nil
        @user.reported = 0
        @user.save
        flash[:notice] = "Unbanned"
      else
        @banned = true
        flash[:notice] = "BANNED"
      end
    end
    @myopendebates = OpenDebate.where(user_id: @user.id).sorted
    @mybinarydebates = BinaryDebate.where(user_id: @user.id).sorted
  end

  def login
  end

  def attempt_login
    if params[:username].present? && params[:password].present?
      located = User.where(:username => params[:username]).first
      if located
        authorized = located.authenticate(params[:password])
      end
    end
    if authorized
      session[:user_id] = authorized.id
      session[:username] = authorized.username
      redirect_to(:action => 'index')
    else
      redirect_to(:action => 'login')
      flash[:notice] = "Incorrect username or password"
    end
  end

  def logout
    session[:user_id] = nil
    session[:username] = nil
    redirect_to(:action => "login")
    flash[:notice] = "You logged out"
  end

  def signup
  end

  def attempt_signup
    if params[:username].present? && params[:password].present? &&
      params[:email].present? && params[:password_confirm].present?
      if params[:password] == params[:password_confirm]
        @new_user = User.new(:email => params[:email], :username => params[:username])
        @new_user.password = params[:password]
        if @new_user.save
          redirect_to(:action => "attempt_login", :username => params[:username], :password => params[:password])
        else
          redirect_to(:action => "signup")
          flash[:notice] = "The password entered is not strong enough"
        end
      else
        redirect_to(:action => "signup")
        flash[:notice] = "Passwords do not match"
      end
    else
      redirect_to(:action => "signup")
      flash[:notice] = "Please fill out all information"
    end
  end

end
