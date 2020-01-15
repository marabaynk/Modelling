//
//  ViewController.swift
//  lab01Random
//
//  Created by Корюн Марабян on 08.10.2019.
//  Copyright © 2019 Корюн Марабян. All rights reserved.
//

import Cocoa

class ViewController: NSViewController, NSApplicationDelegate{
  ///////////////////////////////////////////
    @IBOutlet weak var algTable: NSTableView!
    @IBOutlet weak var tabTable: NSTableView!
    
    @IBOutlet weak var algOneRes: NSTextField!
    @IBOutlet weak var algTwoRes: NSTextField!
    @IBOutlet weak var algThreeRes: NSTextField!
    @IBOutlet weak var tabOneRes: NSTextField!
    @IBOutlet weak var tabTwoRes: NSTextField!
    @IBOutlet weak var tabThreeRes: NSTextField!
    @IBOutlet weak var manRes: NSTextField!
    @IBOutlet weak var warningLabel: NSTextField!
    ///////////////////////////////////////////
    
    @IBOutlet weak var inputTextField: NSTextField!
    //обработка ввода пользователя
    @IBOutlet weak var calcButton: NSButton!
    @IBAction func calcInput(sender:AnyObject) {
        let inputText = inputTextField.stringValue.components(separatedBy: " ").compactMap{Int(String($0))}
        if inputText.isEmpty{
            manRes.stringValue = ""
        }else if inputText.count == 1{
            warningLabel.stringValue = "Введите последовательность чисел!"
            manRes.stringValue = ""
        }else {
            warningLabel.stringValue = ""
            let result = corelation(array: inputText)
            print(result)
            if result.isNaN{
                manRes.stringValue = "1"
            }else{
                manRes.stringValue = String(format: "%.4f", result)
            }
        }
        print(inputText)
    }
///////////////////////////////////////////
    //Обновление таблицы
    @IBAction func refreshTables(_ sender: Any) {
        
    }
///////////////////////////////////////////
    var textArrayOne = [String]()
    var intTextOne = [Int]()
    var intTextOneResult = [Int]()
    
    var textArrayTwo = [String]()
    var intTextTwo = [Int]()
    var intTextTwoResult = [Int]()
    
    var textArrayThree = [String]()
    var intTextThree = [Int]()
    var intTextThreeResult = [Int]()
    
    var algRes = String()
///////////////////////////////////////////
    //Подсчет меры случайности
    func corelation(array: [Int]) -> Double{
        let n = array.count
        if n == 1{
            warningLabel.stringValue = "Введите последовательность чисел!"
            manRes.stringValue = ""
            return 0
        }
        var sumUU = 0
        var sumU = 0
        var sumU2 = 0
        for i in 0...n-1{
            let numj = Int(array[(i+1) % n])
            let numi = Int(array[i])
            
            sumU += numi
            sumU2 += numi * numi
            sumUU += numi * numj
        }
        let top: Double = Double(n * sumUU - sumU * sumU)
        let bottom: Double = Double(n * sumU2 - sumU * sumU)

        let result: Double = top / bottom
        return result
        
    }
    //Табличный метод
    //Для одноразрядных чисел
    func readFromFileOne(){
        if let path = Bundle.main.path(forResource: "random1", ofType: "txt"){
            if let text = try? String(contentsOfFile: path){
                textArrayOne = text.components(separatedBy: "\n")
                intTextOne = textArrayOne.map{ Int($0)!}
            }
        }
        for _ in 1...1000{
            let index = Int.random(in: 0...intTextOne.count-1)
            intTextOneResult.append(intTextOne[index])
        }
    }
    //Для двухразрядных чисел
    func readFromFileTwo(){
        if let path = Bundle.main.path(forResource: "random2", ofType: "txt"){
            if let text = try? String(contentsOfFile: path){
                textArrayTwo = text.components(separatedBy: "\n")
                intTextTwo = textArrayTwo.map{ Int($0)!}
            }
        }
        for _ in 1...1000{
            let index = Int.random(in: 0...intTextTwo.count-1)
            intTextTwoResult.append(intTextTwo[index])
        }
    }
    //Для трехразрядных чисел
    func readFromFileThree(){
        if let path = Bundle.main.path(forResource: "random3", ofType: "txt"){
            if let text = try? String(contentsOfFile: path){
                textArrayThree = text.components(separatedBy: "\n")
                intTextThree = textArrayThree.map{ Int($0)!}
            }
        }
        for _ in 1...1000{
            let index = Int.random(in: 0...intTextThree.count-1)
            intTextThreeResult.append(intTextThree[index])
        }
    }
////////////////////////////////////////
    override func viewDidLoad() {
        super.viewDidLoad()
        algTable.dataSource = self
        algTable.delegate = self
        tabTable.dataSource = self
        tabTable.delegate = self
        //Расчет и вывод табличного метода
        readFromFileOne()
        readFromFileTwo()
        readFromFileThree()
        
        tabOneRes.stringValue = String(format: "%.4f", corelation(array: intTextOneResult))
        tabTwoRes.stringValue = String(format: "%.4f", corelation(array: intTextTwoResult))
        tabThreeRes.stringValue = String(format: "%.4f", corelation(array: intTextThreeResult))

        //corelation(array: testarr)
    }
}
////////////////////////////////////////
extension ViewController: NSTableViewDataSource{
    func numberOfRows(in tableView: NSTableView) -> Int {
        return 10
    }
}

extension ViewController: NSTableViewDelegate{
    //Заполнение таблицы алгоритмическим методом
    func tableView(_ tableView: NSTableView, viewFor tableColumn: NSTableColumn?, row: Int) -> NSView? {
        
        let oneDigit = (1...1000).map({_ in Int.random(in: 1...9)})
        let twoDigit = (1...1000).map({_ in Int.random(in: 10...99)})
        let threeDigit = (1...1000).map({_ in Int.random(in: 100...999)})
        
        algOneRes.stringValue = String(format: "%.4f", corelation(array: oneDigit))
        algTwoRes.stringValue = String(format: "%.4f", corelation(array: twoDigit))
        algThreeRes.stringValue = String(format: "%.4f", corelation(array: threeDigit))

        if tableColumn == algTable.tableColumns[0]{
            let number = tableView.makeView(withIdentifier: tableColumn!.identifier, owner: self) as! NSTableCellView
            number.textField?.intValue = Int32(oneDigit[row])
            return number
        }else if tableColumn == algTable.tableColumns[1]{
            let number = tableView.makeView(withIdentifier: tableColumn!.identifier, owner: self) as! NSTableCellView
            number.textField?.intValue = Int32(twoDigit[row])
            return number
        }else if tableColumn == algTable.tableColumns[2]{
            let number = tableView.makeView(withIdentifier: tableColumn!.identifier, owner: self) as! NSTableCellView
            number.textField?.intValue = Int32(threeDigit[row])
            return number
        }
        ////Заполнение таблицы табличным методом
        else if tableColumn == tabTable.tableColumns[0]{
            let number = tableView.makeView(withIdentifier: tableColumn!.identifier, owner: self) as! NSTableCellView
            number.textField?.intValue = Int32(intTextOneResult[row])
            return number
        }else if tableColumn == tabTable.tableColumns[1]{
            let number = tableView.makeView(withIdentifier: tableColumn!.identifier, owner: self) as! NSTableCellView
            number.textField?.intValue = Int32(intTextTwoResult[row])
            return number
        }else if tableColumn == tabTable.tableColumns[2]{
            let number = tableView.makeView(withIdentifier: tableColumn!.identifier, owner: self) as! NSTableCellView
            number.textField?.intValue = Int32(intTextThreeResult[row])
            return number
        }
    return nil
    }
}
