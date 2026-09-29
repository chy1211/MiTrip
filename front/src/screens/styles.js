import { StyleSheet } from 'react-native';

export const styles = StyleSheet.create({
  titleText: {
    fontSize: 30,
    fontWeight: 'bold',

  },
  desttouch:{
    fontSize: 20,
    fontWeight: 'bold',
    color: '#8E8E8E',
  },
  safeAreaView: {
    flex: 1,
    backgroundColor: 'white',
  },
  scrollView: {
    flex: 1,
    marginHorizontal: 25,
  },
  headerContainer: {
    marginHorizontal: 5,
    flexDirection: 'row',
    justifyContent: 'space-between',
    alignItems: 'center',
    marginBottom: 10,
  },
  headerText: {
    fontSize: 25,
    fontWeight: 'bold',
    color: 'black',
  },
  avatarImage: {
    width: 40,
    height: 40,
  },
  categoriesContainer: {
    flex: 1,
    flexDirection: 'row',
    justifyContent: 'center',
    alignItems: 'center',
    paddingHorizontal: 16,
    paddingVertical: 10,
  },
  container: {
    flexDirection: 'row',
    alignItems: 'center',
    justifyContent: 'space-between',
    paddingHorizontal: 12,
    paddingVertical: 10,
    marginTop: 10,
  },
  row:{
    flexDirection: 'row',
    alignContent: 'center',
    justifyContent: 'center',
    flex: 1,
    backgroundColor: 'black',
    borderRadius: 8,
    width: 400,
    height: 60,
  },
  tough:{
    marginHorizontal: 60,
    justifyContent: 'center',
  },
  centeredElement: {
    flex: 1,
    alignItems: 'center',
  },
  headerRightContent: {
    flexDirection: 'row',
    alignItems: 'flex-end',
  },
  absoluteCenter: {
    position: 'absolute',
    left: 0,
    right: 0,
    justifyContent: 'center',
    alignItems: 'center',
  },
  categoriesContainer2: {
    flexDirection: 'row',
    paddingHorizontal: 20,
    // backgroundColor: '#E0E0E0',
    borderRadius: 8,
    alignItems: 'center',
    justifyContent: 'space-around',
    height: 50,
  },
  buttonContainer: {
    flex: 1,
    // backgroundColor: '#E0E0E0',
    // paddingHorizontal: 20, // Add padding to create space between buttons
    alignContent: 'center',
    justifyContent: 'center',
  
  },
  button: {
    borderWidth: 1,
    // borderColor: '#E0E0E0',
    // marginHorizontal: 20, // Add margin to create space between buttons
    justifyContent: 'center',
    alignItems: 'center',
    paddingVertical:6,
  },
});