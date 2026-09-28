using System;
using System.Collections.Generic;
using System.ComponentModel;
using System.Data;
using System.Drawing;
using System.Linq;
using System.Text;
using System.Threading.Tasks;
using System.Windows.Forms;
using System.Threading;
using System.Threading.Channels;


namespace channel_token
{
    public partial class Form1 : Form
    {
        Channel<string> channel = Channel.CreateBounded<string>(100);

        CancellationTokenSource token;

        public Form1()
        {
            InitializeComponent();
        }

        private async void button1_Click(object sender, EventArgs e)  // input
        {
            string input = textBox3.Text;
            await channel.Writer.WriteAsync(input);
            textBox1.AppendText("input: " + input + Environment.NewLine);
            
        }

        private async void button2_Click(object sender, EventArgs e)  // output
        {
            token = new CancellationTokenSource();

            int len = channel.Reader.Count;
            //if (len > 0)
            //{
            //    string get_str = await channel.Reader.ReadAsync();
            //    textBox2.AppendText("output: " + get_str + Environment.NewLine);
            //}
            //else
            //{
            //    textBox2.AppendText("데이터가 없습니다." + Environment.NewLine);
            //}
            try
            {
                while (!token.Token.IsCancellationRequested)
                {
                    string get_str = await channel.Reader.ReadAsync(token.Token);
                    textBox2.AppendText("output: " + get_str + Environment.NewLine);
                }
            }
            catch (Exception ex) { }

        }

        private void button3_Click(object sender, EventArgs e)  // 종료
        {
            token.Cancel();
            
        }
    }
}
