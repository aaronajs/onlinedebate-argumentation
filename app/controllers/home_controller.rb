class HomeController < ApplicationController

  # user cannot access any page except rules of conduct and home pages unless logged in
  before_action :confirm_logged_in, :except => [:rules, :index]
  # user cannot access any page except rules of conduct page unless not banned
  before_action :confirm_not_banned, :except => [:rules]

  # navigates to home page - shows all debates
  def index
    @users = User.sorted
    @open = OpenDebate.sorted
    @binary = BinaryDebate.sorted
  end

  # navigates to rules of conduct page
  def rules
  end

  # navigates to the show page
  # has different attributes and settings per debate type
  def show
    type = params[:type]
    if type == "open"
      show_open
    else
      show_binary
    end
  end

  # adds a new argument to a debate, specifying its attributes
  # argument is leading
  # argument is added to a for or against list if part of a binary debate
  # the debate is updated, and redirected to the show page after the evaluation script is called
  def add_new_argument
    if arg_params[:description].present?
      debateid = params[:debate_id]
      argument = Argument.new()
      argument.description = arg_params[:description]
      argument.debate_id = debateid
      if params[:type] == "open"
        argument.isOpen = true
      else
        argument.isOpen = false
      end
      argument.isLeading = true
      argument.user_id = session[:user_id]
      argument.save
      if params[:type] == "binary"
        debate = BinaryDebate.find(debateid)
        if arg_params[:choice] == "for"
          debate.for_arguments.push(argument.id)
        else
          debate.against_arguments.push(argument.id)
        end
        update_debate(debate)
      else
        debate = OpenDebate.find(debateid)
        update_debate(debate)
      end
      evaluation(params[:type], params[:debate_id])
      redirect_to({:action => 'show', :id => params[:debate_id], :type => params[:type]})
      flash[:notice] = "Added new argument"
    else
      redirect_to({:action => 'show', :id => params[:debate_id], :type => params[:type]})
      flash[:notice] = "Fill in argument description"
    end
  end

  # adds a new counter argument to a debate, specifying its attributes
  # argument is added to a for or against list if part of a binary debate
  # the debate is updated, and redirected to the show page after the evaluation script is called
  def add_argument
    type = params[:type]
    if arg_params[:description].present?
      argument = Argument.find(params[:arg])
      arg = Argument.new(arg_params)
      arg.debate_id = params[:debate]
      if type == "open"
        arg.isOpen = true
        debate = OpenDebate.find(params[:debate])
      else
        arg.isOpen = false
        debate = BinaryDebate.find(params[:debate])
      end
      arg.isLeading = false
      arg.user_id = session[:user_id]
      arg.save
      if type != "open"
        if debate.for_arguments.include?(argument.id)
          debate.for_arguments.push(arg.id)
        else
          debate.against_arguments.push(arg.id)
        end
      end
      argument.attacks.push(arg.id)
      update_debate(debate)
      if argument.save
        evaluation(type, params[:debate ])
        redirect_to({:action => 'show', :id => params[:debate], :type => type})
        flash[:notice] = "Added counter argument"
      else
        redirect_to({:action => 'show', :id => params[:debate], :type => type})
        flash[:notice] = "Unable to add argument"
      end
    else
      redirect_to({:action => 'show', :id => params[:debate], :type => type})
      flash[:notice] = "Fill in counter argument description"
    end
  end

  # updates the updated_at column of a debate
  def update_debate(debate)
    debate.updated_at = DateTime.now
    debate.save
  end

  # marks or unmarks an argument as relevant for a particular user
  # redirects to the show page after the evaluation script is called
  def upvote
    @arg = Argument.find(params[:arg_id])
    @type = params[:type]
    @user = User.find(session[:user_id])
    if @user.voted_for? @arg
      @arg.unliked_by @user
      flash[:notice] = "Unmarked relevant"
    else
      @arg.vote_by :voter => @user, :vote => 'like'
      flash[:notice] = "Marked relevant"
    end
    evaluation(@type, params[:debate_id])
    redirect_to({:action => 'show', :id => params[:debate_id], :type => @type})
  end

  # marks or unmarks an argument as irrelevant for a particular user
  # redirects to the show page after the evaluation script is called
  def downvote
    @arg = Argument.find(params[:arg_id])
    @type = params[:type]
    @user = User.find(session[:user_id])
    if @user.voted_for? @arg
      @arg.undisliked_by @user
      flash[:notice] = "Unmarked irrelevant"
    else
      @arg.vote_by :voter => @user, :vote => 'bad'
      flash[:notice] = "Marked irrelevant"
    end
    evaluation(@type, params[:debate_id])
    redirect_to({:action => 'show', :id => params[:debate_id], :type => @type})
  end

  # navigates to the new page
  def new
  end

  # creates a debate based on its type
  def create
    if deb_params[:description].present?
      if deb_params[:type] == "open"
        create_open
      else
        create_binary
      end
    else
      redirect_to(:action => 'new')
      flash[:notice] = "Fill in debate description"
    end
  end

  # reports an argument and the user that created it
  # redirects to the show page after the evaluation script is called
  def report_arg
    arg = Argument.find(params[:arg_id])
    arg.reported = arg.reported + 1
    arg.save
    report_user(arg.user_id)
    evaluation(params[:type], params[:debate_id])
    redirect_to({:action => 'show', :id => params[:debate_id], :type => params[:type]})
    flash[:notice] = "Reported argument"
  end

  # reports a debate and the user that created it
  # redirects to the show page after the evaluation script is called
  def report_deb
    if params[:type] == "open"
      deb = OpenDebate.find(params[:deb_id])
    else
      deb = BinaryDebate.find(params[:deb_id])
    end
    deb.reported = deb.reported + 1
    deb.save
    report_user(deb.user_id)
    evaluation(params[:type], params[:deb_id])
    redirect_to({:action => 'show', :id => params[:deb_id], :type => params[:type]})
    flash[:notice] = "Reported debate"
  end

  private

  # reports a user
  # if they are passed the ban threshold, they have a ban date set - banned for 7 days
  def report_user(id)
    user = User.find(id)
    user.reported = user.reported + 1
    if user.reported >= 10
      user.ban_date = Date.today
    end
    user.save
  end

  # calls the evaluation script appropriate for the debate type
  # obtains all the arguments for that debate
  def evaluation(type, debate)
    if type == "open"
      arguments = Argument.where(debate_id: debate, isOpen: true)
    else
      arguments = Argument.where(debate_id: debate, isOpen: false)
    end
    removedLowRating = arguments.reject {|x| x.weighted_score <= -10}
    filteredArguments = removedLowRating.reject {|x| x.reported >= 10}

    if type == "open"
      open_evaluation(debate, filteredArguments)
    else
      binary_evaluation(debate, filteredArguments)
    end
  end

  # calls the python script to evaluate open debates
  # converts to json before passing arguments to script
  # obtains result from script to set new leader for debate
  def open_evaluation(debate, arguments)
    full = ''
    arguments.each do |arg|
      full = full + "\'" + arg.create_json.to_json + "\' "
    end
    result = `python lib/assets/evaluate_open.py #{full}`
    debate = OpenDebate.find(debate)
    debate.leader = result.to_i
    debate.save
  end

  # calls the python script to evaluate binary debates
  # converts to json before passing arguments to script
  # obtains result from script to set new leading side for debate
  def binary_evaluation(debate, arguments)
    puts "binary evaluation"
    full = ''
    arguments.each do |arg|
      full = full + "\'" + arg.create_json.to_json + "\' "
    end

    debate = BinaryDebate.find(debate)
    forargs = debate.for_arguments.to_json
    againstargs = debate.against_arguments.to_json

    result = `python lib/assets/evaluate_binary.py #{forargs} #{againstargs} #{full}`
    puts result
    if result.to_i == 1
      debate.isFor = true
    else
      debate.isFor = false
    end
    debate.save
  end

  # creates and stores an open debate
  # redirects to the show page
  def create_open
    @debate = OpenDebate.new()
    @debate.description = deb_params[:description]
    @debate.user_id = session[:user_id]
    if @debate.save
      redirect_to(:action => 'show', :id => @debate.id, :type => deb_params[:type])
    else
      redirect_to(:action => 'new')
      flash[:notice] = "Couldn't save open debate"
    end
  end

  # creates and stores an binary debate
  # redirects to the show page
  def create_binary
    if deb_params[:for].present? && deb_params[:against].present?
      @debate = BinaryDebate.new()
      @debate.for = deb_params[:for]
      @debate.against = deb_params[:against]
      @debate.description = deb_params[:description]
      @debate.user_id = session[:user_id]
      if @debate.save
        redirect_to(:action => 'show', :id => @debate.id, :type => deb_params[:type])
      else
        redirect_to(:action => 'new')
        flash[:notice] = "Couldn't save binary debate"
      end
    else
      redirect_to(:action => 'new')
      flash[:notice] = "Add for and against options"
    end
  end

  # shows page with debate information and its arguments for an open debate
  # redirects to show page
  def show_open
    @type = params[:type]
    @debate = OpenDebate.find(params[:id])
    @user = User.find(@debate.user_id)
    @arguments = Argument.where(debate_id: @debate.id, isOpen: true).sorted
  end

  # shows page with debate information and its arguments for a binary debate
  # redirects to show page
  def show_binary
    @type = params[:type]
    @debate = BinaryDebate.find(params[:id])
    @user = User.find(@debate.user_id)
    @arguments = Argument.where(debate_id: @debate.id, isOpen: false).sorted
  end

  # stores parameters of an argument
  def arg_params
    params.require(:argument).permit(:description, :choice)
  end

  # stores parameters of a debate
  def deb_params
    params.require(:debate).permit(:type, :description, :for, :against)
  end

end
