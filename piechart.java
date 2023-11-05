import javafx.application.Application;
import javafx.collections.FXCollections;
import javafx.collections.ObservableList;
import javafx.scene.Scene;
import javafx.stage.Stage;
import javafx.scene.chart.*;
import javafx.scene.Group;

public class PieChartSample extends Application{
    @Override public void start(Stage stage){
        Scene scene = new Scene(new Group());
        stage.setTitle("Mood");
        stage.setWidth(500);
        stage.setHeight(500);

        ObservableList<PieChart.Data> pieChartData=
            FXCollections.observableArrayList(
            new PieChart.Data("Happy", );
            new PieChart.Data("Sad", );

            );
        final PieChart chart = new PieChart(pieChartData);
        chart.setTitle("Mood");

        ((Group) scene.getRoot()).getChildren().add(chart);
        stage.setScene(scene);
        stage.show();
    }
    public static void main(String[]args){
        launch(args);
    }
}