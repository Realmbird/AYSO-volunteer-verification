class PlayersController < ApplicationController
    def show
        @player = Player.find(params[:id])
    end
    
    def edit
        @player = Player.find(params[:id])
    end
  
    def update
        @player = Player.find(params[:id])
        if @player.update(player_params)
            redirect_to player_path(@player), notice: 'Player was successfully updated.'
        else
            render :edit
        end
    end
    
    private
    
    def player_params
        params.require(:player).permit(:program_name, :division_name, :team_name, :order_payment_status, :postal_code, :city, :state, :player_first_name, :player_last_name, :player_gender, :player_birth_date, :street_address, :unit, :user_email, :telephone, :cellphone, :other_phone, :order_date, :order_no, :order_detail_description, :orderitem_amount, :orderitem_amount_paid, :orderitem_balance)
    end
end
